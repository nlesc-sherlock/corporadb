from pyspark.ml.clustering import LDA
from pyspark.ml.linalg import SparseVector
from pyspark.sql import Row
from scipy.io import mmread
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import multiprocessing
import argparse

# Always use all available cores
cpus = multiprocessing.cpu_count()
sc = SparkContext("local[" + str(cpus) + "]", "Simple App1")
spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
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
    # rowRange = sc.parallelize(xrange(10))
    dataSpark = spark.createDataFrame(rowRange
            .map(lambda i: Row(label=i, features=sparkToScipySparse(data.getrow(i)))))
    lda = LDA(k=k, maxIter=iterations)
    model = lda.fit(dataSpark)
    model.save(savemodel)

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
