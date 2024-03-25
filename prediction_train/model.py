import torch
import torch.nn as nn
import torch.nn.functional as F

img2me = lambda x, y : torch.mean((x - y) ** 2)

class NeuralNetwork(nn.Module):

    def __init__(self, input_dim, output_dim, D=5, W=200, skips=[2]):
        super().__init__()

        self.skips = skips
        self.network_linears = nn.ModuleList(
            [nn.Linear(input_dim, W)] +
            [nn.Linear(W, W) if i not in skips else nn.Linear(W + input_dim, W)
             for i in range(D - 1)]
        )

        ## output head, 2 for amplitude and phase
        self.network_output = nn.Linear(W, output_dim)

    def forward(self, network_input):
        
        x = network_input

        for i, layer in enumerate(self.network_linears):
            x = F.relu(layer(x))
            if i in self.skips:
                x = torch.cat([network_input, x], -1)

        outputs = self.network_output(x)    # (batch_size, 2)
        return outputs