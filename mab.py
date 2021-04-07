import random


class MAB:

    def __init__(self, *, state):
        """
        :param state: dictionary with current state of the model {'1':{}, '2': {}...}

        :param n_arms: how many strategies we start with
        :param arms_probability: probabilities for strategies
        :param arms_dict_params: arms description
        :param active_arms: which arms are active (turn on)
        """
        self.arms_dict_params = state
        self.arms_probability = None

    @property
    def n_arms(self):
        return len(self.arms_dict_params)

    @property
    def active_arms(self):
        return [i for i in self.arms_dict_params if self.arms_dict_params.get(i).get('is_active')]


    def add_arms(self):
        """
        Add new strategy
        :return:
        """
        print(self.number_active_strategies)
        self.arms_dict_params.update({str(self.n_arms + 1): {'description': '',
                                                              'current_alpha': 1,
                                                              'current_beta': 1,
                                                              'success': [0],
                                                              'trials': [0],
                                                              'probability': [],
                                                              'is_active': 1,
                                                              'params_weight': None,
                                                              'is_filled': False
                                                               }
                                      })
        return self.arms_dict_params

    def results_from_db(self, gp_conn):
        """
        tmp method for loading rewards from DB

        :return gp_conn: connection to DB
        :return: dict with rewards per arm
        """
        d = dict.fromkeys(self.active_arms)
        for i in d:
            d[i] = {'success': None, 'trials': None}
            d[i]['success'] = random.randint(0, 100)
            d[i]['trials'] = random.randint(100, 200)
        return d

    def arms_probabilities(self):
        """
        Get probabilities for strategies according the reward

        :return: the dict with probabilities for each active strategy
        """
        self.arms_probability = dict.fromkeys(self.active_arms)
        for i in self.arms_probability:
            self.arms_probability[i] = random.betavariate(self.arms_dict_params[i]['current_alpha'],
                                                          self.arms_dict_params[i]['current_beta'])
            self.arms_dict_params[i]['probability'].append(self.arms_probability[i])

        return self.arms_dict_params, self.arms_probability

    def update_distribution(self):
        """
        Updating params of Beta distribution according the rewards. Alpha incresed by positive reward, beta - by non-positive.

        :return: updated dict with strategies
        """
        results = self.results_from_db()

        for i in self.active_arms:
            try:
                self.arms_dict_params[i]['success'].append(results[i]['success'])
                self.arms_dict_params[i]['trials'].append(results[i]['trials'])
                self.arms_dict_params[i]['current_alpha'] += self.arms_dict_params[i]['success'][-1]
                self.arms_dict_params[i]['current_beta'] += self.arms_dict_params[i]['trials'][-1] - \
                                                                 self.arms_dict_params[i]['success'][-1]
            except:
                # вот тут надо рэйзить ошибку
                self.arms_dict_params[i]['success'].append(0)
                self.arms_dict_params[i]['trials'].append(0)

        return self.arms_dict_params

    def update_distr_and_return_proba(self, gp_conn):
        """
        Updating params of Beta distribution according the rewards. Alpha incresed by positive reward, beta - by non-positive.
        :param gp_conn: DB connection
        :return: updated dict with strategies, probabilities for strategies
        """        

        results = self.results_from_db(gp_conn)
        self.arms_probability = dict.fromkeys(self.active_arms)

        for i in self.active_arms:
            try:
                self.arms_dict_params[i]['success'].append(results[i]['success'])
                self.arms_dict_params[i]['trials'].append(results[i]['trials'])
                self.arms_dict_params[i]['current_alpha'] += self.arms_dict_params[i]['success'][-1]
                self.arms_dict_params[i]['current_beta'] += self.arms_dict_params[i]['trials'][-1] - \
                                                            self.arms_dict_params[i]['success'][-1]
            except:
                # вот тут надо рэйзить ошибку
                self.arms_dict_params[i]['success'].append(0)
                self.arms_dict_params[i]['trials'].append(0)

            self.arms_probability[i] = random.betavariate(self.arms_dict_params[i]['current_alpha'],
                                                          self.arms_dict_params[i]['current_beta'])
            self.arms_dict_params[i]['probability'].append(self.arms_probability[i])

        return self.arms_dict_params, self.arms_probability

    def remove_arm(self, arm):
        """
        Remove strategy

        :param arm: Strategy id
        :return: number of active strategies
        """
        print(self.number_active_strategies)
        self.active_arms.remove(arm)
        self.arms_dict_params[arm]['is_active'] = 0

        return self.arms_dict_params, self.number_active_strategies

    @property
    def number_active_strategies(self):
        """
        Count active strategies

        :return:
        """
        return len(self.active_arms)

    def strategy_weights_description(self, arms=[], weights_dicts=[None], descs=['']):
        """
        Adding strategy description

        :param arms: strategy ids list, like ['1', '2'...]
        :param descs: list of descriptions for arms, like ['ascending price', 'descending purchases cnt'...]
        :param weights_dicts: dict with feature's weights, like {'sale': 10, 'cnt_web_purchases': 5, 'cnt_reviews': -10}}

        :return: saving descriptions
        """
        for a, w, d in zip(arms, weights_dicts, descs):
            self.arms_dict_params[a]['description'] = d

            self.arms_dict_params[a]['params_weight'] = w
            self.arms_dict_params[a]['is_filled'] = True
        return self.arms_dict_params

    def turn_on_arm(self, arm):
        """
        :param arm: strategy id to turn on
        :return:
        """
        print(self.number_active_strategies)
        self.arms_dict_params[arm]['is_active'] = 1

        return self.arms_dict_params, self.number_active_strategies
