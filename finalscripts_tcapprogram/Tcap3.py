import imgpros
import sys
import utilities
import model
import results

utilities.intializer(sys.argv)
utilities.preview()
imgpros.crop()
model.analyze()
model.compute()
results.save()