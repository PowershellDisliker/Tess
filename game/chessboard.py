from typing import Tuple

from game.common import MOVE_RESPONSE, PIECE_TYPE, ChessPiece, Move, get_index, add_tuples, get_coords
from game.setup import get_starting_board, get_piece_square_tables

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
UR, DR, DL, UL        = (-1, 1), (1, 1), (1, -1), (-1, -1)

class ChessBoard:
    def __init__(self) -> None:
        self.WIDTH = 8
        self.HEIGHT = 8
        self.PLAYER_1 = 1
        self.PLAYER_2 = 2

        self.current_player = self.PLAYER_1
        self.running = True
        self.winner: int | None = None
        
        self.tiles: list[ChessPiece | None] = get_starting_board(self.PLAYER_1, self.PLAYER_2)
        self.piece_square_tables: dict[Tuple[PIECE_TYPE, int], list[int]] = get_piece_square_tables()

        self.moves_list: list[Move] = []

        self.total_mat_score = self.get_material_score(self.PLAYER_1)
        self.total_position_score = len(self.get_player_pieces(self.PLAYER_1)) * 50

    
    def get_player_pieces(self, player: int) -> list[Tuple[int, int]]:
        if player not in [1, 2]:
            return []
        
        player_pieces = []
        for i, tile in enumerate(self.tiles):
            if tile is not None and tile.owner == player:
                player_pieces.append(get_coords(i))
                
        return player_pieces


    def get_player_king(self, player: int) -> Tuple[int, int] | None:
        if player not in [1, 2]:
            return

        for i, tile in enumerate(self.tiles):       
            if tile is not None and tile.piece_type == PIECE_TYPE.KING and tile.owner == player:
                return get_coords(i)

    
    def get_piece_moves(self, source: Tuple[int, int]) -> list[Move]:
        return [move for move in self.__get_unchecked_piece_moves(source) if self.__check_piece_movement(move)]


    def double_moved_pawn_at(self, source: Tuple[int, int]) -> bool:
        if len(self.moves_list) == 0:
            return False
        return self.moves_list[-1].double_moved_pawn == source

    
    def make_move(self, move: Move) -> MOVE_RESPONSE:
        if not self.__validate_piece_movement(move):
            return MOVE_RESPONSE.INVALID_MOVEMENT

        if not self.__check_piece_movement(move):
            return MOVE_RESPONSE.INVALID_PUTS_SELF_IN_CHECK

        moving_player = self.current_player

        response = self.__make_move(move)

        if self.check_for_checkmate(self.current_player):
            self.running = False
            self.winner = moving_player
            return response

        if self.check_for_stalemate(self.current_player):
            self.running = False
            return response
        
        return response


    def undo_move(self) -> bool:
        if not self.moves_list:
            return False

        move: Move = self.moves_list.pop()

        success, piece = self.get_piece(move.destination)

        if not success or not piece:
            return False

        self.__move_piece(move.destination, move.source)

        piece.moved = move.moved

        if move.taken_piece:
            self.__set_piece(move.taken_piece[1], move.taken_piece[0])

        if move.castled_rook:
            self.__move_piece(move.castled_rook[1], move.castled_rook[0])

            success, rook = self.get_piece(move.castled_rook[0])

            if success and rook:
                rook.moved = False

        if move.promotion:
            piece.piece_type = PIECE_TYPE.PAWN

        self.current_player = self.PLAYER_1 if self.current_player != self.PLAYER_1 else self.PLAYER_2
        self.running = True
        self.winner = None

        return True


    def check_for_check(self, player: int) -> bool:
        player_king = self.get_player_king(player)

        if not player_king:
            return False

        success, piece = self.get_piece(player_king)

        if not success or piece is None:
            return False

        long_h = [add_tuples(LEFT, LEFT), add_tuples(RIGHT, RIGHT)]
        long_v = [add_tuples(UP, UP), add_tuples(DOWN, DOWN)]
        combos = [[long_h, [UP, DOWN]], [long_v, [LEFT, RIGHT]]]

        # Knights
        for combo in combos:
            for lon in combo[0]:
                for sho in combo[1]:
                    diff = add_tuples(lon, sho)
                    success, inner_piece = self.get_piece(add_tuples(player_king, diff))
                    if success and inner_piece and inner_piece.piece_type == PIECE_TYPE.KNIGHT and inner_piece.owner != player:
                        return True
        # Pawns        
        for tile in [(piece.direction, 1), (piece.direction, -1)]:
            success, pawn_tile = self.get_piece(add_tuples(tile, player_king))

            if success and pawn_tile and pawn_tile.owner != player and pawn_tile.piece_type == PIECE_TYPE.PAWN:
                return True

        straights: list[Tuple[int, int]] = [UP, DOWN, LEFT, RIGHT]
        diags: list[Tuple[int, int]] = [UL, DL, UR, DR]

        for straight in straights:
            pos = add_tuples(player_king, straight)
            success, in_tile = self.get_piece(pos)

            while success and not in_tile:
                pos = add_tuples(pos, straight)
                success, in_tile = self.get_piece(pos)
            
            if success and in_tile and in_tile.owner != player and in_tile.piece_type in [PIECE_TYPE.ROOK, PIECE_TYPE.QUEEN]:
                return True

        for diag in diags:
            pos = add_tuples(player_king, diag)
            success, in_tile = self.get_piece(pos)

            while success and not in_tile:
                pos = add_tuples(pos, diag)
                success, in_tile = self.get_piece(pos)

            if success and in_tile and in_tile.owner != player and in_tile.piece_type in [PIECE_TYPE.BISHOP, PIECE_TYPE.QUEEN]:
                return True
        return False


    def check_for_checkmate(self, player: int) -> bool:
        in_check = self.check_for_check(player)

        if not in_check:
            return False

        player_pieces = self.get_player_pieces(player)
        
        for piece in player_pieces:
            if self.get_piece_moves(piece):
                return False
        return True

    
    def check_for_stalemate(self, player: int) -> bool:
        for piece in self.get_player_pieces(player):
            if self.get_piece_moves(piece):
                return False
        return not self.check_for_check(player)


    def get_turn_number(self) -> int:
        return len(self.moves_list)


    def get_piece(self, coords: Tuple[int, int]) -> Tuple[bool, ChessPiece | None]:
        index = get_index(coords)

        if index is None:
            return False, None

        tile = self.tiles[index]

        return True, tile
    

    def __set_piece(self, coords: Tuple[int, int], piece: ChessPiece | None) -> Tuple[bool, ChessPiece | None]:
        index = get_index(coords)

        if index is None:
            return (False, None)

        old = self.tiles[index]
        self.tiles[index] = piece

        return (True, old)


    def __move_piece(self, source: Tuple[int, int], dest: Tuple[int, int]) -> Tuple[bool, ChessPiece | None]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return (False, None)

        a, old = self.__set_piece(dest, piece)
        b, _ = self.__set_piece(source, None)

        piece.set_moved()

        if a and b:
            return (True, old)
        return (False, None)


    def __make_move(self, move: Move) -> MOVE_RESPONSE:
        success, piece = self.get_piece(move.source)

        if not success:
            return MOVE_RESPONSE.INVALID_ERROR_FETCHING_TILE

        if not piece:
            return MOVE_RESPONSE.INVALID_TILE_IS_NONE

        if piece.owner != self.current_player:
            return MOVE_RESPONSE.INVALID_OUT_OF_TURN

        if move.taken_piece:
            self.__set_piece(move.taken_piece[1], None)

        self.__move_piece(move.source, move.destination)

        if move.promotion:
            piece.piece_type = move.promotion

        if move.castled_rook:
            self.__move_piece(move.castled_rook[0], move.castled_rook[1])

        self.current_player = self.PLAYER_1 if self.current_player != self.PLAYER_1 else self.PLAYER_2

        self.moves_list.append(move)
        return MOVE_RESPONSE.SUCCESS


    # All Commands to do with piece checking / verification
    def __check_piece_movement(self, move: Move) -> bool:
        self.__make_move(move)
        in_check = self.check_for_check(self.PLAYER_1 if self.current_player != self.PLAYER_1 else self.PLAYER_2)
        self.undo_move()

        return not in_check


    def __validate_piece_movement(self, move: Move) -> bool:
        valid_moves = self.get_piece_moves(move.source)
        return move in valid_moves


    def __get_unchecked_piece_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        match piece.piece_type:
            case PIECE_TYPE.PAWN:
                valid_moves = self.__get_valid_pawn_moves(source)
            case PIECE_TYPE.ROOK:
                valid_moves = self.__get_valid_rook_moves(source)
            case PIECE_TYPE.KNIGHT:
                valid_moves = self.__get_valid_knight_moves(source)
            case PIECE_TYPE.BISHOP:
                valid_moves = self.__get_valid_bishop_moves(source)
            case PIECE_TYPE.QUEEN:
                valid_moves = self.__get_valid_queen_moves(source)
            case PIECE_TYPE.KING:
                valid_moves = self.__get_valid_king_moves(source)

        return valid_moves


    def __get_valid_pawn_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []

        valid_moves: list[Move] = []

        single_forward = add_tuples(source, (piece.direction, 0))
        double_forward = add_tuples(source, (piece.direction * 2, 0))
        attacking_squares = [add_tuples(source, (piece.direction, -1)), add_tuples(source, (piece.direction, 1))]
        
        success, forward_tile = self.get_piece(single_forward)

        promotion_pieces = [PIECE_TYPE.KNIGHT, PIECE_TYPE.BISHOP, PIECE_TYPE.ROOK, PIECE_TYPE.QUEEN]

        if success and forward_tile is None:
            if single_forward[0] in [0, 7]:
                for promotion_piece in promotion_pieces:
                    valid_moves.append(Move(source, single_forward, piece.moved, promotion=promotion_piece))
            valid_moves.append(Move(source, single_forward, piece.moved))
            
            success, double_forward_tile = self.get_piece(double_forward)

            if success and source[0] in [1, 6] and double_forward_tile is None:
                valid_moves.append(Move(source, double_forward, piece.moved, double_moved_pawn=double_forward))

        for pos in attacking_squares:
            success, attacked_tile = self.get_piece(pos)

            behind = add_tuples(pos, (-piece.direction, 0))
            success, behind_tile = self.get_piece(behind)

            if (attacked_tile is not None and attacked_tile.owner != piece.owner):
                if pos[0] in [0, 7]:
                    for promotion_piece in promotion_pieces:
                        valid_moves.append(Move(source, pos, piece.moved, promotion=promotion_piece, taken_piece=(attacked_tile, pos)))
                valid_moves.append(Move(source, pos, piece.moved, taken_piece=(attacked_tile, pos)))

            if attacked_tile is None and behind_tile is not None and self.double_moved_pawn_at(behind) and behind_tile.owner != piece.owner and behind_tile.piece_type == PIECE_TYPE.PAWN:
                if pos[0] in [0, 7]:
                    for promotion_piece in promotion_pieces:
                        valid_moves.append(Move(source, pos, piece.moved, promotion=promotion_piece, taken_piece=(behind_tile, behind)))
                else:
                    valid_moves.append(Move(source, pos, piece.moved, taken_piece=(behind_tile, behind)))

        return valid_moves


    def __get_valid_rook_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        valid_moves: list[Move] = []

        for direction in [RIGHT, DOWN, LEFT, UP]:
            pos = source

            while True:
                pos = add_tuples(pos, direction)
                success, tile = self.get_piece(pos)

                if not success:
                    break

                if tile is None:
                    valid_moves.append(Move(source, pos, piece.moved))
                
                elif tile.owner != piece.owner:
                    valid_moves.append(Move(source, pos, piece.moved, taken_piece=(tile, pos)))
                    break

                else:
                    break
        
        return valid_moves


    def __get_valid_knight_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        h_long = [add_tuples(LEFT, LEFT), add_tuples(RIGHT, RIGHT)]
        h_short = [LEFT, RIGHT]
        v_long = [add_tuples(UP, UP), add_tuples(DOWN, DOWN)]
        v_short = [UP, DOWN]

        combos = [[h_long, v_short], [v_long, h_short]]

        valid_moves: list[Move] = []

        for combo in combos:
            for lon in combo[0]:
                for sho in combo[1]:
                    pos = add_tuples(source, add_tuples(lon, sho))
                    success, tile = self.get_piece(pos)

                    if not success:
                        continue

                    if tile is None:
                        valid_moves.append(Move(source, pos, piece.moved))

                    elif tile.owner != piece.owner:
                        valid_moves.append(Move(source, pos, piece.moved, taken_piece=(tile, pos)))

        return valid_moves


    def __get_valid_bishop_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        directions = [UL, UR, DL, DR]

        valid_moves: list[Move] = []

        for direction in directions:
            pos = source
            while True:
                pos = add_tuples(pos, direction)
                success, tile = self.get_piece(pos)

                if not success:
                    break

                if tile is None:
                    valid_moves.append(Move(source, pos, piece.moved))

                elif tile.owner != piece.owner:
                    valid_moves.append(Move(source, pos, piece.moved, taken_piece=(tile, pos)))
                    break

                else:
                    break

        return valid_moves
                

    def __get_valid_queen_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        directions = [UP, DOWN, LEFT, RIGHT, UL, DL, UR, DR]

        valid_moves: list[Move] = []

        for direction in directions:
            pos = source

            while True:
                pos = add_tuples(pos, direction)
                success, tile = self.get_piece(pos)

                if not success:
                    break

                if tile is None:
                    valid_moves.append(Move(source, pos, piece.moved))
                
                elif tile.owner != piece.owner:
                    valid_moves.append(Move(source, pos, piece.moved, taken_piece=(tile, pos)))
                    break

                else:
                    break

        return valid_moves


    def __get_valid_king_moves(self, source: Tuple[int, int]) -> list[Move]:
        success, piece = self.get_piece(source)

        if not success or piece is None:
            return []
        
        directions = [UP, DOWN, LEFT, RIGHT, UR, DR, DL, UL]

        valid_moves: list[Move] = []

        for direction in directions:
            pos = source

            pos = add_tuples(pos, direction)
            success, tile = self.get_piece(pos)

            if not success:
                continue

            if tile is None:
                valid_moves.append(Move(source, pos, piece.moved))

            elif tile.owner != piece.owner:
                valid_moves.append(Move(source, pos, piece.moved, taken_piece=(tile, pos)))

        if not piece.moved:
            l_success, l_rook = self.get_piece((source[0], 0))
            r_success, r_rook = self.get_piece((source[0], 7))

            if l_rook is not None and l_rook.piece_type == PIECE_TYPE.ROOK and l_rook.owner == piece.owner and not l_rook.moved:
                pos = source
                should_add = True

                for _ in range(3):
                    pos = add_tuples(pos, LEFT)
                    success, inner_piece = self.get_piece(pos)

                    if success and inner_piece is not None:
                        should_add = False
                
                if should_add:
                    valid_moves.append(Move(source, (source[0], 2), piece.moved, castled_rook=((source[0], 0), (source[0], 3))))

            if r_rook is not None and r_rook.piece_type == PIECE_TYPE.ROOK and r_rook.owner == piece.owner and not r_rook.moved:
                pos = source
                should_add = True

                for _ in range(2):
                    pos = add_tuples(pos, RIGHT)
                    success, inner_piece = self.get_piece(pos)

                    if success and inner_piece is not None:
                        should_add = False

                if should_add:
                    valid_moves.append(Move(source, (source[0], 6), piece.moved, castled_rook=((source[0], 7), (source[0], 5))))

        return valid_moves

    
    def print_state(self) -> None:
        print(f"Current Player {self.current_player}")
        print(f"Turn Number: {self.get_turn_number()}")
        print(f"Tiles: {["Empty" if tile is None else tile.piece_type for tile in self.tiles[:10]]}")
        print(f"Move list: {[f"{move.source} -> {move.destination}" for move in self.moves_list[-3:]]}")
        print(f"Winner: {self.winner}")


    def get_material_score(self, player: int) -> int:
        values = {
            PIECE_TYPE.PAWN: 1, PIECE_TYPE.BISHOP: 3, PIECE_TYPE.KNIGHT: 3,
            PIECE_TYPE.ROOK: 5, PIECE_TYPE.QUEEN: 9, PIECE_TYPE.KING: 100
        }
        total = 0
        for pos in self.get_player_pieces(player):
            _, piece = self.get_piece(pos)
            if piece:
                total += values.get(piece.piece_type, 0)
        return total


    def get_position_score(self, player: int) -> int:
        value = 0

        for pos in self.get_player_pieces(player):
            success, piece = self.get_piece(pos)
            index = get_index(pos)

            if success and piece and index:
                value += self.piece_square_tables[(piece.piece_type, player)][index]
    
        return value

    def get_score(self, current_depth: int) -> float:
        if self.check_for_checkmate(self.current_player):
            return -1000.0 + current_depth if self.current_player == 1 else 1000.0 - current_depth

        if self.check_for_stalemate(self.current_player):
            return 0.0

        mat_score = float(self.get_material_score(self.PLAYER_1) - self.get_material_score(self.PLAYER_2)) / self.total_mat_score
        position_score = float(self.get_position_score(self.PLAYER_1) - self.get_position_score(self.PLAYER_2)) / self.total_position_score
        check_score = 0.0

        if self.check_for_check(self.PLAYER_1): check_score -= 1
        if self.check_for_check(self.PLAYER_2): check_score += 1
        
        mat_weight: float = 0.6
        position_weight: float = 0.2
        check_weight: float = 0.2

        return (mat_score * mat_weight) + (position_score * position_weight) + (check_score * check_weight)