import merge from 'lodash/object/merge'
import forEach from 'lodash/collection/forEach'
// loosely based on the awesome redux real-world example from
// https://github.com/rackt/redux/blob/master/examples/real-world/middleware/api.js

function simplify (x) {
  return {type: x.type, id: x.id}
}

export default function format_jsonapi_result (input, key) {
  const entitiesMap = {}
  const result = {}
  const output = { entities: entitiesMap }
  const addToMap = (x) => {
    if (!entitiesMap[x.type]) { entitiesMap[x.type] = {} }

    let toAdd = simplify(x)
    if (x.attributes) toAdd = merge(toAdd, x.attributes)
    if (x.relationships) toAdd = merge(toAdd, extract_relationships(x))

    entitiesMap[x.type][x.id] = toAdd
  }
  const extract_relationships = (data) => {
    const relationships = {}
    forEach(data.relationships || {}, (n, key) => {
      if (Array.isArray(n.data)) {
        relationships[key] = []
        forEach(n.data, (x) => {
          addToMap(x)
          relationships[key].push(simplify(x))
        })
      } else {
        addToMap(n.data)
        relationships[key] = simplify(n.data)
      }
    })

    return relationships
  }

  if (input.included) {
    forEach(input.included, addToMap)
  }

  if (input.meta) { result.meta = input.meta };
  if (input.links) { result.links = input.links };

  if (input.data) {
    if (Array.isArray(input.data)) {
      result.data = []
      forEach(input.data, x => {
        addToMap(x)
        result.data.push(simplify(x))
      })
    } else {
      addToMap(input.data)
      result.data = simplify(input.data)
    }
  }
  if (!key) { key = 'stream' }

  output[key] = result
  return output
}
