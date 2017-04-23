from numpy import mean, var, std

# accuracy
x = [72.73, 81.82, 54.55, 45.45, 63.64, 45.45, 81.82, 54.55, 81.82, 63.64]

m = mean(x) # general average
v = var(x) # dispersion
s = std(x) # standard deviation

# confidence interval
print(m)
print(m - s, m + s)