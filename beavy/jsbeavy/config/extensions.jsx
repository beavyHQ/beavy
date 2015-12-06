/*eslint-disable no-throw-literal */
// our extensions collection
// not exported, please use the helper functions below
const extensions = {}

function getOrDefault (key, df) {
  if (!extensions[key]) {
    extensions[key] = df
  }
  return extensions[key]
}

// dictionary based

export function addNamedExtension (key, name, item) {
  let base = getOrDefault(key, {})
  if (base[name]) {
    throw 'Name ' + name + ' has already been registerd for ' + key
  }
  base[name] = item
}

export function getNamedExtensions (key) {
  return extensions[key] || {}
}

// list based
export function insertExtension (key, position, item) {
  let base = getOrDefault(key, [])
  base.splice(position, 0, item)
}

export function addManyExtensions (key, items) {
  extensions[key] = getOrDefault(key, []).concat(items)
}

export function addExtension (key, item) {
  let base = getOrDefault(key, [])
  base.push(item)
}

export function getExtensions (key) {
  return extensions[key] || []
}
