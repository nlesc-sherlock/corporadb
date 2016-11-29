from pyspark.ml.clustering import LDA
from pyspark.ml.linalg import SparseVector
from pyspark.sql import Row
from scipy.io import mmread, mmwrite
import numpy as np
import argparse

from pyspark import SparkContext
from pyspark.sql.session import SparkSession

sc = SparkContext("local[4]", "Simple App1")
spark = SparkSession.builder \
     .getOrCreate()

def sparkToScipySparse(spRow):
    '''Convert scipy.sparse to spark.sparse vector'''
    cols = spRow.shape[1]
    indices = spRow.indices
    values = spRow.data
    return SparseVector(cols, { idx: val for idx,val in zip(indices, values) })

def trainModel(docMatrix, savemodel, k, iterations=10):
    data = mmread(docMatrix)
    rowRange = sc.parallelize(xrange(data.shape[0]))
    dataSpark = spark.createDataFrame(rowRange
            .map(lambda i: Row(label=i, features=sparkToScipySparse(data.getrow(i)))))
    lda = LDA(k=k, maxIter=iterations)
    model = lda.fit(dataSpark)
    model.save(savemodel)

    topicMatrix = model.topicsMatrix().toArray()
    topicMatrix = topicMatrix.T
    topicMatrix = topicMatrix / topicMatrix.sum(axis=0)
    print 'TODO: give wordXtopic.mtx a path'
    mmwrite('wordXtopic.mtx', topicMatrix)

    print 'TODO: give docXtopic.mtx a path'
    docXTopics = model.transform(dataSpark)
    dxT = docXTopics.collect()
    dxT_v2 = np.array([ dxtI['topicDistribution'] for dxtI in dxT ])
    mmwrite('docXtopic.mtx', dxT_v2)

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tokenize and create dictionary out of given files")
    parser.add_argument('input_matrix')
    parser.add_argument('output_model')
    parser.add_argument('number_topics', type=int)
    parser.add_argument('number_iterations', type=int)
    args = parser.parse_args()

    docMatrix = args.input_matrix  # 'enron_mail_random_clean.mtx'
    savemodel = args.output_model  # 'enron_mail_clean.lda.model'
    nTopics = args.number_topics   # 5
    nIterations = args.number_iterations # 10,000

    trainModel(docMatrix, savemodel, nTopics, nIterations)
