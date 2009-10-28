'''
Example from rpy2

http://rpy.sourceforge.net/rpy2/doc/html/introduction.html
'''
import rpy2.robjects as robjects

r = robjects.r

m = r.matrix(r.rnorm(100), ncol=5)
pca = r.princomp(m)
r.plot(pca, main="Eigen values")
#r.biplot(pca, main="biplot")
