__author__ = "Christian Hideki Maekawa, Rafael de Carvalho Miranda and Carlos Henrique Valério de Moraes"
__copyright__ = "Sponsor by FAPEMIG from 2017 - 2019, Project: Utilização de métodos de metamodelagem para resolução de problemas complexos em otimização via simulação"
__credits__ = [
    "Christian Hideki Maekawa, Rafael de Carvalho Miranda and Carlos Henrique Valério de Moraes"
]
__license__ = "MIT"
__version__ = "0.1.0"
__cite__ = "http://www.fmepro.org/XP/XP-EasyArtigos/Site/Uploads/Evento21/TrabalhosCompletosDOC/VII-030.pdf"


# This is a new version using pytorch instead C#(deprecated AForge). Was made 100% by Christian Hideki Maekawa. 	

# This is a new version using pytorch instead C#(deprecated AForge). Was made 100% by Christian Hideki Maekawa.

# Inspired and researched with Rafael de Carvalho Miranda and Carlos Henrique Valério de Moraes
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from pathlib import Path


class metamodel:
    def __init__(self, file_name="./datasets/data.csv"):
        self.file_name = file_name
        self.df = self.load_dataframe(Path.cwd() / file_name)
        self.model = None
        self.train_losses = []
        self.test_losses = []
        self.X_test = None
        self.y_test = None

    def cuda_status(self):
        print(f"Are you using GPU? {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(torch.cuda.get_device_name())
            print(f"GPU Power(max,min){torch.cuda.get_device_capability(device=None)}")

    def load_dataframe(self, file_name):
        df = pd.read_csv(file_name)
        return df

    def plot_correlations(self):
        plt.rcParams["figure.figsize"] = [15, 15]
        x_axis = len(self.df.iloc[:, 0])
        x = np.linspace(0, x_axis, x_axis)
        axs = scatter_matrix(self.df)
        n = len(self.df.columns)
        for x in range(n):
            for y in range(n):
                # to get the axis of subplots
                ax = axs[x, y]
                # to make x axis name vertical
                ax.xaxis.label.set_rotation(90)
                # to make y axis name horizontal
                ax.yaxis.label.set_rotation(0)
                # to make sure y axis names are outside the plot area
                ax.yaxis.labelpad = 50
        # #plt.show()

    def plot_distributions(self):
        # plt.rcParams["figure.figsize"] = [15, 15]
        self.df.hist()
        # #plt.show()

    def get_data(self):
        X = self.df.iloc[:, 0:5].values
        y = self.df.iloc[:, -1].values
        return X, y

    def split_data(self, X, y, test_size=0.8):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        return X_train, X_test, y_train, y_test

    def fit(self, mid_layer=5, epochs=1000, learning_rate=0.01):
        def train(model, criterion, optimizer, X_train, y_train, epochs=1000):
            train_losses = np.zeros(epochs)
            test_losses = np.zeros(epochs)
            for it in range(epochs):
                optimizer.zero_grad()

                outputs = model(X_train)
                loss = criterion(outputs, y_train)

                loss.backward()
                optimizer.step()
                outputs_test = model(X_test)
                loss_test = criterion(outputs_test, y_test)
                train_losses[it] = loss.item()
                test_losses[it] = loss_test.item()
            if (it + 1) % 50 == 0:
                print(
                    f"Progress {((it + 1)/epochs)*100}%, Train Loss: {loss.item():.4f} Test Loss: {loss_test.item():.4f}"
                )
            self.model = model
            return train_losses, test_losses

        X, y = self.get_data()
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        N, D = X_train.shape
        model = nn.Sequential(
            nn.Linear(D, mid_layer), nn.Sigmoid(), nn.Linear(mid_layer, 1)
        )
        X_train = torch.from_numpy(X_train.astype(np.float32))
        X_test = torch.from_numpy(X_test.astype(np.float32))
        y_train = torch.from_numpy(y_train.astype(np.float32).reshape(-1, 1))
        y_test = torch.from_numpy(y_test.astype(np.float32).reshape(-1, 1))
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        X_train = torch.from_numpy(X.astype(np.float32))
        y_train = torch.from_numpy(y.astype(np.float32).reshape(-1, 1))
        self.train_losses, self.test_losses = train(
            model, criterion, optimizer, X_train, y_train, epochs
        )
        self.X_test = X_test
        self.y_test = y_test
        return self.model

    def predict(self, X_test):
        with torch.no_grad():
            if type(X_test) == list:
                X_test = torch.from_numpy(np.array([X_test]).astype(np.float32))
                # print(X_test)
            if type(X_test) == np.ndarray:
                X_test = torch.from_numpy(X_test.astype(np.float32))
            y_pred = self.model(X_test)
            y_pred = y_pred.numpy()
        return y_pred


    # def train_performance(self):
        # if (
        #         (self.model != None)
        #         or (len(self.train_losses) != 0)
        #         or (len(self.test_losses) != 0)
        # ):
        # # plt.plot(self.train_losses)
        # # plt.plot(self.test_losses)
        # # #plt.show()
        # else:
        #     assert (
        #             (self.model != None)
        #             or (len(self.train_losses) != 0)
        #             or (len(self.test_losses) != 0)
        #     ), f"Apply fit before run performance."

    def train_performance(self):
        if (
            (self.model != None)
            or (len(self.train_losses) != 0)
            or (len(self.test_losses) != 0)
        ):
            plt.plot(self.train_losses)
            plt.plot(self.test_losses)
            # plt.show()
        else:
            assert (
                (self.model != None)
                or (len(self.train_losses) != 0)
                or (len(self.test_losses) != 0)
            ), f"Apply fit before run performance."


    def model_peformance(self):
        if self.model != None:
            with torch.no_grad():
                line_x = np.linspace(0, len(self.X_test), len(self.X_test))
                y_pred = self.predict(self.X_test)
                # plt.scatter(line_x, self.y_test, label="Expected")
                # plt.scatter(line_x, y_pred, label="Predicted")
                # #plt.show()
        else:
            assert (
                (self.model != None)
                or (len(self.train_losses) != 0)
                or (len(self.test_losses) != 0)
            ), f"Apply fit before run performance."
