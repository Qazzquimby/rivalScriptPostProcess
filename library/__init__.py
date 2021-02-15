import itertools

from library import attacks, caching, comparisons, data_structures, debugging, dynamics, inits, mutations, sprites, \
    transitions, watches

library_modules = [attacks, caching, comparisons, data_structures, debugging, dynamics, inits, mutations, sprites,
                   transitions, watches]

dependencies = set(itertools.chain.from_iterable(
    [library_module.DEPENDENCIES for library_module in library_modules]
))
