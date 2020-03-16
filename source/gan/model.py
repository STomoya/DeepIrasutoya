
import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

class Generator(nn.Module):
    def __init__(self, latent_dim, img_shape=(3, 64, 64), use_leaky=False, normalize=False):
        super(Generator, self).__init__()
        self.img_shape = img_shape

        def block(in_feat, out_feat, use_leaky, normalize):
            layers = [nn.Linear(in_feat, out_feat)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_feat))
            if use_leaky:
                layers.append(nn.LeakyReLU(0.2, inplace=True))
            else:
                layers.append(nn.ReLU(inplace=True))
            return layers

        self.model = nn.Sequential(
            *block(latent_dim, 128, use_leaky=use_leaky, normalize=normalize),
            *block(128, 256, use_leaky=use_leaky, normalize=normalize),
            *block(256, 512, use_leaky=use_leaky, normalize=normalize),
            *block(512, 1024, use_leaky=use_leaky, normalize=normalize),
            nn.Linear(1024, int(np.prod(img_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        img = img.view(img.size(0), *self.img_shape)
        return img


class Discriminator(nn.Module):
    def __init__(self, img_shape, use_leaky=False, normalize=False):
        super(Discriminator, self).__init__()
        self.img_shape = img_shape

        def block(in_feat, out_feat, use_leaky, normalize):
            layers = [nn.Linear(in_feat, out_feat)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_feat))
            if use_leaky:
                layers.append(nn.LeakyReLU(0.2, inplace=True))
            else:
                layers.append(nn.ReLU(inplace=True))
            return layers


        self.model = nn.Sequential(
            *block(int(np.prod(self.img_shape)), 512, use_leaky=use_leaky, normalize=normalize),
            *block(512, 256, use_leaky=use_leaky, normalize=normalize),
            nn.Linear(256, 1),
            nn.Sigmoid(),
        )

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        validity = self.model(img_flat)

        return validity