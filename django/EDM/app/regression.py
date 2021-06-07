import numpy as np

# reference: https://www.geeksforgeeks.org/linear-regression-python-implementation/
# https://www.highcharts.com/blog/tutorials/calculating-and-drawing-a-linear-regression-using-highcharts/

def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)

def calculate(X, Y):
    x = np.array(X)
    y = np.array(Y)

    b = estimate_coef(x, y)

    y_pred = b[0] + b[1]*x

    x = x.tolist()
    y = y.tolist()

    x1 = min(x)
    x2 = max(x)

    min_y = min(y)
    max_y = max(y)

    y1 = b[0] + b[1] * x1
    y2 = b[0] + b[1] * x2

    scatter = [[_x, _y] for _x, _y in zip(x, y)]

    data = {
        'min_x': x1, 'max_x': x2,
        'min_y': min_y, 'max_y': max_y,
        'line': [[x1, y1], [x2, y2]],
        'scatter': scatter
    }

    return data # plot attributes: scatter(x, y) + plot(x, y_pred)