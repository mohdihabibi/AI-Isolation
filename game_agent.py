"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import operator


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
    # TODO: finish this function!
    # if game.is_loser(player):
    #     return float("-inf")
    #
    # if game.is_winner(player):
    #     return float("inf")
    #
    # if not game.get_player_location(player):
    #     return 0
    # if not game.get_player_location(game.get_opponent(player)):
    #     return 0
    #
    # weight = 0
    # first_layer = [(0,1), (0,-1), (1,0), (-1, 0)]
    # second_layer = [(0,2), (0, -2), (2,0), (-2,0)]
    # third_layer = [(0, 3), (0, -3), (3, 0), (-3, 0)]
    # for move in game.get_legal_moves(player):
    #     for position in first_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight -=3
    #     for position in second_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight -=2
    #     for position in third_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight -=1
    #
    # for move in game.get_legal_moves(game.get_opponent(player)):
    #     for position in first_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight +=3
    #     for position in second_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight +=2
    #     for position in third_layer:
    #         if not ((0,0) <= tuple(map(operator.add,move,position)) <= (game.width, game.height)):
    #             weight +=1
    #
    #
    #
    #
    # return float(weight)
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_location = game.get_player_location(game.get_opponent(player))
    if opp_location == None:
        return 0.

    own_location = game.get_player_location(player)
    if own_location == None:
        return 0.

    return float(abs(sum(opp_location) - sum(own_location)))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This function will calculate the intersection of
    player move and opponent move. It will return a percentage of

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
    # TODO: finish this function!

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    if not game.get_legal_moves(player):
        return game.utility(player)

    if not game.get_legal_moves(game.get_opponent(player)):
        return game.utility(game.get_opponent(player))

    player_legal_moves = game.get_legal_moves(player)

    opponent_legal_moves = game.get_legal_moves(game.get_opponent(player))

    identical_moves = list(set(player_legal_moves)&set(opponent_legal_moves))
    return float((len(identical_moves)/len(player_legal_moves))*100)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player. This function calculate the heuristic value base on
    the player position and the opponent position. This will return a bigger number
    if the distance is bigger.

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
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    if not game.get_player_location(player):
        return 0

    if not game.get_player_location(game.get_opponent(player)):
        return 0

    player_location = sum(game.get_player_location(player))
    opponent_location = sum(game.get_player_location(game.get_opponent(player)))

    return float(abs(player_location-opponent_location))


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
            return best_move
            # pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        IsolationPlayer.__init__(self, search_depth, score_fn, timeout)

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

        # TODO: finish this function!
        best_score = float("-inf")
        best_move = (-1,-1)

        if len(game.get_legal_moves(self)) == 0:
            return best_move

        for move in game.get_legal_moves():
            v = self.min_val(game.forecast_move(move), depth-1)
            if v > best_score:
                best_score = v
                best_move = move
        return best_move

    def min_val(self, game , depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # if not game.get_legal_moves():
        #     return 1
        if depth == 0:
            return self.score(game, self)
        v = float("inf")
        for move in game.get_legal_moves():
            v = min(v, self.max_val(game.forecast_move(move), depth-1))
        return v

    def max_val(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # if not game.get_legal_moves(self):
        #     return -1
        if depth == 0:
            return self.score(game, self)
        v = float("-inf")
        for move in game.get_legal_moves():
            v = max(v, self.min_val(game.forecast_move(move), depth-1))
        return v


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

        if len(game.get_legal_moves()) == 0:
            return best_move

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for d in range(1,len(game.get_blank_spaces())):
                move = self.alphabeta(game, d)
                if move == ():
                    return best_move
                else:
                    best_move = move

        except SearchTimeout:
            return best_move
            # pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

        # TODO: finish this function!

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

        # TODO: finish this function!
        best_score = float("-inf")
        best_move = (-1,-1)
        for move in game.get_legal_moves(self):
            v = self.max_val(game, depth, alpha, beta)
            if v > best_score:
                best_score = v
                best_move = move
            if v >= beta:
                return best_move
            alpha = max(alpha, v)
        return best_move

    def max_val(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        v = float("-inf")
        for move in game.get_legal_moves(self):
            v = max(v, self.min_val(game.forecast_move(move), depth-1, alpha, beta))

            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_val(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        v = float("+inf")
        for move in game.get_legal_moves(self):
            v = min(v, self.max_val(game.forecast_move(move), depth-1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v