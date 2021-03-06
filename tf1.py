import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


'''
input >weight > hidden layer 1 (activation function) > weights > hidden l 2 (
activation function) > weights > output layer

compare output to intended output > cost or loss function (cross entropy)
optimization function (optimizer) . minimize cost (adamOptimizer ... SGD, 
adaGrade)



feed foward + backprop = epoch
Data goes in, it is compared and then backpropogation happens, this is one 
cycle and several happen. The one cycle is called an epoch
'''


mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# the first hidden layer has 500 nodes
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10
batch_size = 100

# 784 pixels per data
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def neural_network_model(data):
    # input_data * weights + biases
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784,
                                                               n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1,
                                                               n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2,
                                                               n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3,
                                                               n_classes])),
                      'biases': tf.Variable(tf.random_normal([n_classes]))}

    # ends up having a shape of data size * 500
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer[
        'biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer[
        'biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_2_layer['weights']), hidden_3_layer[
        'biases'])
    l3 = tf.nn.relu(l3)

    output = tf.add(tf.matmul(l3, output_layer['weights']), output_layer[
        'biases'])

    return output

def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits = prediction, labels = y))
    # default value of lr is 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    hm_epochs = 10

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                # c is the cost tensor is evaluated and
                # the result of the optimizer tensor is ignored
                _, c = sess.run([optimizer, cost], feed_dict = {x:epoch_x,
                                                                y:epoch_y})
                epoch_loss += c
            print('Epoch', epoch, 'competed out of', hm_epochs, 'loss:',
                  epoch_loss)

        # argmax gives the index of the biggest value on some axis
        # 1 is the horizontal axis
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        ### following are equivalent
        #print(sess.run(accuracy,
        #               feed_dict={x: mnist.test.images,
        # y_: mnist.test.labels}))

        print('Acurracy:', accuracy.eval({x:mnist.test.images,
        y:mnist.test.labels}))

train_neural_network(x)