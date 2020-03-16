import torch
from torchvision.utils import save_image
import numpy as np

def train(
    dataset,
    epochs,
    latent_dim,
    G,
    G_optim,
    D,
    D_optim,
    criterion,
    device,
    sample_interval
):
    history = {
        'g_loss' : [],
        'd_loss' : []
    }

    for epoch in range(epochs):
        for index, images in enumerate(dataset, start=1):
            # labels
            real = np.ones((images.size(0),))
            fake = np.zeros((images.size(0),))
            real = torch.from_numpy(real).type(torch.FloatTensor).to(device)
            fake = torch.from_numpy(fake).type(torch.FloatTensor).to(device)

            # real images
            images = images.type(torch.FloatTensor).to(device)

            '''
            Generator training
            '''

            # input noise
            z = np.random.normal(loc=0.0, scale=1.0, size=(images.size(0), latent_dim))
            z = torch.from_numpy(z).type(torch.FloatTensor).to(device)

            # generate images
            generated = G(z)

            # generator loss
            g_loss = criterion(D(generated), real)

            # back propagation
            G_optim.zero_grad()
            g_loss.backward()
            G_optim.step()

            '''
            Discriminator training
            '''
            
            # discriminator loss
            real_loss = criterion(D(images),    real)
            fake_loss = criterion(D(generated.detach()), fake)
            d_loss = (real_loss + fake_loss) / 2

            # back propagation
            D_optim.zero_grad()
            d_loss.backward()
            D_optim.step()

            # save losses
            history['g_loss'].append(g_loss.item())
            history['d_loss'].append(d_loss.item())

            batches_done = epoch * len(dataset) + index
            if batches_done % sample_interval == 0:
                print('EPOCH : {}/{}\tBATCH : {}/{}'.format(epoch,epochs,index,len(dataset)))
                print('\tG loss : {:.5f}\tD loss : {:.5f}'.format(g_loss.item(), d_loss.item()))
                save_image(generated.data[0], 'result/batch_{}.jpg'.format(batches_done), normalize=True)

    return history, G.cpu()