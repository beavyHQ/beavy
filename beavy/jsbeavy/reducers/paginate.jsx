import merge from 'lodash/object/merge'
import union from 'lodash/array/union'
import map from 'lodash/collection/map'

// based on the ideas of the real world example of rackt/redux:
// https://github.com/rackt/redux/blob/master/examples/real-world/reducers/paginate.js

// Creates a reducer managing pagination, given the action types to handle,
// and a function telling how to extract the key from an action.
export default function paginate ({ types, mapActionToKey }) {
  if (!Array.isArray(types) || types.length !== 3) {
    throw new Error('Expected types to be an array of three elements.')
  }
  if (!types.every(t => typeof t === 'string')) {
    throw new Error('Expected types to be strings.')
  }
  if (typeof mapActionToKey !== 'function') {
    throw new Error('Expected mapActionToKey to be a function.')
  }

  const [requestType, successType, failureType] = types

  function updatePagination (state = {
    isFetching: false,
    meta: {},
    links: {},
    data: []
  }, action, key) {
    switch (action.type) {
      case requestType:
        return merge({}, state, {
          isFetching: true
        })
      case successType:
        const incoming = action.response[key]
        return merge({}, state, {
          isFetching: false,
          data: union(state.data, incoming.data),
          meta: merge(state.meta, incoming.meta),
          links: merge(state.links, incoming.links)
        })
      case failureType:
        return merge({}, state, {
          isFetching: false
        })
      default:
        return state
    }
  }

  return function updatePaginationByKey (state = {}, action) {
    switch (action.type) {
      case requestType:
      case successType:
      case failureType:
        const key = mapActionToKey(action)
        if (typeof key !== 'string') {
          throw new Error('Expected key to be a string.')
        }
        return merge({}, state, updatePagination(state, action, key))
      default:
        return state
    }
  }
}
