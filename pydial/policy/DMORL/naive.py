###############################################################################
# PyDial: Multi-domain Statistical Spoken Dialogue System Software
###############################################################################
"""
Implementation of Naive MODQN - Multi-Objective Deep Q Network

The algorithm is developed with Pytorch

Author: Runzhe Yang
"""


import torch
import torch.nn as nn
import torch.nn.functional as F


class NaiveLinearCQN(torch.nn.Module):
    '''
        Linear Controllable Q-Network, Naive Version
    '''

    def __init__(self, state_size, action_size, reward_size):
        super(NaiveLinearCQN, self).__init__()

        self.state_size = state_size
        self.action_size = action_size
        self.reward_size = reward_size

        # S x A -> (W -> R). =>. S x W -> (A -> R)
        self.affine1 = nn.Linear(state_size + reward_size,
                                 (state_size + reward_size) * 16)
        self.affine2 = nn.Linear((state_size + reward_size) * 16,
                                 (state_size + reward_size) * 32)
        self.affine3 = nn.Linear((state_size + reward_size) * 32,
                                 (state_size + reward_size) * 32)
        # self.affine4 = nn.Linear((state_size + reward_size) * 64,
        #                          (state_size + reward_size) * 32)
        self.affine5 = nn.Linear((state_size + reward_size) * 32,
                                 action_size)

    def forward(self, state, preference, execmask=None):
        x = torch.cat((state, preference), dim=1)
        x = x.view(x.size(0), -1)
        x = F.relu(self.affine1(x))
        x = F.relu(self.affine2(x))
        x = F.relu(self.affine3(x))
        # x = F.relu(self.affine4(x))
        q = self.affine5(x)
        if execmask is not None:
            q = torch.add(q, execmask)
        hq = q.detach().max(dim=1)[0]
        return hq, q