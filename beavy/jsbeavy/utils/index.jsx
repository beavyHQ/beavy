/* global __CONFIG__HOME_URL, __CONFIG__URLS */

export function createConstants (...constants) {
  return constants.reduce((acc, constant) => {
    acc[constant] = constant
    return acc
  }, {})
}

export function getStoreEntity (state, item) {
  return state.entities[item.type][item.id]
}

function makePrefixUrlMaker (prefix) {
  if (prefix.slice(-1) !== '/') {
    prefix += '/'
  }
  return function makeUrl (inp) {
    let url = prefix + inp
    if (url.slice(-1) !== '/') {
      url += '/'
    }
    if (url === __CONFIG__HOME_URL) { return '/' }
    return url
  }
}

export const make_url = (function (cfg) {
  const urlMakers = {}
  for (var key in cfg) {
    if (cfg.hasOwnProperty(key)) {
      urlMakers[key.toLowerCase()] = makePrefixUrlMaker(cfg[key])
    }
  }
  return urlMakers
})(__CONFIG__URLS)
