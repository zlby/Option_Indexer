raise ImportError("This module is marked as deprecated by Alan")

from algorithm.interval.net_graph_build import *

def get_interval(code1, code2, graph, options=None):
    if options is None:
        pass
        # r1 = dl.get_option_rate_list(code1)
        # r2 = dl.get_option_rate_list(code2)
        #
        # p1 = dl.get_option_price_list(code1)
        # p2 = dl.get_option_price_list(code2)
    # elif options is data.CombineOptionsDataProvider:
    else:
        r1 = options(code=code1, attribute="vol")
        r2 = options(code=code2, attribute="vol")
        p1 = options(code=code1, attribute="price")
        p2 = options(code=code2, attribute="price")
    # else:
    #     raise data.UnSupportDataFormatError()

    sample_size = len(r1)

    def train_sim_normal_distribution_args(sess, loop_count):
        for i in range(loop_count):
            sess.run(graph.train_step, feed_dict={graph.inputs: [r1, r2, p1, p2]})

    with tf.Session(graph=graph.g) as sess:
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter("./logs", sess.graph)
        sess.run(graph.init)
        train_sim_normal_distribution_args(sess, 500)

        for i in range(500):
            sess.run(graph.train_step, feed_dict={graph.inputs: [r1, r2, p1, p2]})
            if i % 2 == 0:
                rs = sess.run(merged, feed_dict={graph.inputs: [r1, r2, p1, p2]})
                writer.add_summary(rs, i)
                writer.flush()

        bene_y = []

        for i in range(500):
            results = sess.run([graph.trd_train, graph.bene], feed_dict={graph.inputs: [r1, r2, p1, p2]})
            if i % 2 == 0:
                rs = sess.run(merged, feed_dict={graph.inputs: [r1, r2, p1, p2]})
                writer.add_summary(rs, i)
                writer.flush()
                bene_y.append(results[1])



        # import matplotlib.pyplot as plt
        # plt.scatter([index for index,_ in enumerate(bene_y)], bene_y, linewidths=0.2)
        # plt.show()

        res = sess.run([graph.interval_nm, graph.interval_hg, graph.interval_err, graph.trd_err, graph.scl], feed_dict={graph.inputs: [r1, r2, p1, p2]})
        return res[:3]

# print(get_interval('m1708-c-2500', 'm1708-c-2600'))

    # bene_y = []
    # for t in range(500):
    #     for i in range(2):
    #         sess.run(trd_train, feed_dict={inputs: [r1, r2, p1, p2]})
    #     bene_y += [(sess.run(bene, feed_dict={inputs: [r1, r2, p1, p2]}))]
    # # res = sess.run([out_hg, out_nm, dr_prob, max_raw_p, bene, trd_hg, trd_nm], feed_dict={inputs: [r1, r2, p1, p2]})
    # import matplotlib.pyplot as plt
    #
    # plt.plot([x for x in range(500)], bene_y, 'r-')
    # print(bene_y[-1])
    # plt.show()


    # import matplotlib.pyplot as plt
    # # fg = plt.gcf()
    # plt.plot([i for i, e in enumerate(res[0])], res[0], "b")
    # plt.plot([i for i, e in enumerate(res[1])], res[1], "r")
    # plt.plot([i for i, e in enumerate(res[2])], res[2], "g")
    # plt.plot(res[0], res[1])
    # plt.plot(res[0], res[2])
    # plt.show()
