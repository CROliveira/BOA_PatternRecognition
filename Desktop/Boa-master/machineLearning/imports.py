# ML Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.plotting import category_scatter, plot_decision_regions
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, accuracy_score
from yellowbrick.classifier import ConfusionMatrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_blobs, make_moons
from sklearn.naive_bayes import GaussianNB
from collections import Counter
from scipy.stats import mode
from scipy.spatial.distance import cdist
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import GradientBoostingClassifier
from dataHarvesting import properties_file as pf
