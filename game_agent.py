"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import isolation

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    cur_move = game.get_player_location(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    nxt_move_score = len(own_moves) - len(opp_moves)

    # if my current move is also reachable by the opponent,
    # prefer that location over another location with the same number of own moves
    opp_move_bonus = 0
    if cur_move in opp_moves:
        opp_move_bonus = 8

    return nxt_move_score + opp_move_bonus


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    cur_move = game.get_player_location(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    nxt_move_score = len(own_moves) - (len(opp_moves) * 2)

    # if my current move is also reachable by the opponent,
    # prefer that location over another location with the same number of own moves
    opp_move_bonus = 0
    if cur_move in opp_moves:
        opp_move_bonus = 8

    return nxt_move_score + opp_move_bonus # + cur_move_corner_bonus


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    cur_move = game.get_player_location(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    nxt_move_score = len(own_moves) - len(opp_moves)

    # prefer center of the board for the current move
    cur_move_corner_bonus = corner_score(game, cur_move) * 8

    return nxt_move_score + cur_move_corner_bonus


# if current move is at the edge of the board, score = 0
# if current move is 1 slot away from the edge of the board, score = 0.5
# else score = 1
def corner_score(game, move):
    y, x = move
    if x <= 0 or x >= game.width - 1 or y <= 0 or y >= game.height - 1:
        return 0.0
    elif x <= 1 or x >= game.width - 2 or y <= 1 or y >= game.height - 2:
        return 0.5
    else:
        return 1.0


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        default_move = (-1, -1)

        if depth <= 0:
            return default_move

        player_legal_moves = game.get_legal_moves(self)

        if len(player_legal_moves) == 1:
            return player_legal_moves[0]

        best_max_score = float("-inf")
        best_max_score_move = default_move

        for player_move in player_legal_moves:
            current_score = self.min_score(game.forecast_move(player_move), depth - 1)
            if best_max_score < current_score:
                best_max_score = current_score
                best_max_score_move = player_move

        return best_max_score_move

    def max_score(self, game, depth):
        """
        Returns the max score from the player's move
        :param game:
        :param depth:
        :return: player's max score
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal condition: if we reached the bottom (depth=0), return current score
        if depth <= 0:
            return self.score(game, self)

        # max node maximizes score based on the PLAYER's move
        player_legal_moves = game.get_legal_moves(self)

        best_max_score = float("-inf")

        for player_move in player_legal_moves:
            best_max_score = max(best_max_score, self.min_score(game.forecast_move(player_move), depth - 1))

        return best_max_score

    def min_score(self, game, depth):
        """
        Returns the min score from the opponent's move
        :param game:
        :param depth:
        :return: opponent's min score
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal condition: if we reached the bottom (depth=0), return current score
        if depth <= 0:
            return self.score(game, self)

        # min node minimizes score based on the OPPONENT's move
        opponent_legal_moves = game.get_legal_moves(game.get_opponent(self))

        best_min_score = float("inf")

        for opponent_move in opponent_legal_moves:
            best_min_score = min(best_min_score, self.max_score(game.forecast_move(opponent_move), depth - 1))

        return best_min_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        depth = 0

        try:
            # Keep iterating until the time is up
            while self.time_left() > self.TIMER_THRESHOLD:
                depth += 1
                best_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        default_move = (-1, -1)

        if depth <= 0:
            return default_move

        player_legal_moves = game.get_legal_moves(self)

        if len(player_legal_moves) == 1:
            return player_legal_moves[0]

        best_max_score = float("-inf")
        best_max_score_move = default_move

        for player_move in player_legal_moves:
            current_score = self.min_score(game.forecast_move(player_move), depth - 1, alpha, beta)
            if best_max_score < current_score:
                best_max_score = current_score
                best_max_score_move = player_move
            if beta <= best_max_score:
                break
            alpha = max(alpha, best_max_score)

        return best_max_score_move

    def max_score(self, game, depth, alpha, beta):
        """
        Returns the max score from the player's move
        :param game:
        :param depth:
        :param alpha:
        :param beta:
        :return: player's max score
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal condition: if we reached the bottom (depth=0), return current score
        if depth <= 0:
            return self.score(game, self)

        # max node maximizes score based on the PLAYER's move
        player_legal_moves = game.get_legal_moves(self)

        best_max_score = float("-inf")

        for player_move in player_legal_moves:
            best_max_score = max(best_max_score, self.min_score(game.forecast_move(player_move), depth - 1, alpha, beta))
            if beta <= best_max_score:
                break
            alpha = max(alpha, best_max_score)

        return best_max_score

    def min_score(self, game, depth, alpha, beta):
        """
        Returns the min score from the opponent's move
        :param game:
        :param depth:
        :param alpha:
        :param beta:
        :return: opponent's min score
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal condition: if we reached the bottom (depth=0), return current score
        if depth <= 0:
            return self.score(game, self)

        # min node minimizes score based on the OPPONENT's move
        opponent_legal_moves = game.get_legal_moves(game.get_opponent(self))

        best_min_score = float("inf")

        for opponent_move in opponent_legal_moves:
            best_min_score = min(best_min_score, self.max_score(game.forecast_move(opponent_move), depth - 1, alpha, beta))
            if alpha >= best_min_score:
                break
            beta = min(beta, best_min_score)

        return best_min_score
