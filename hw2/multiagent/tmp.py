        def search_depth(state, depth, agent):
            if agent == state.getNumAgents():
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else:
                    return search_depth(state, depth + 1, 0)
            else:
                actions = state.getLegalActions(agent)

                if len(actions) == 0:
                    return self.evaluationFunction(state)

                next_states = (search_depth(state.generateSuccessor(agent, action),
                               depth, agent + 1)
                               for action in actions)

                return (max if agent == 0 else min)(next_states)

        return max(gameState.getLegalActions(0),
                   key = lambda x: search_depth(gameState.generateSuccessor(0, x), 1, 1))
