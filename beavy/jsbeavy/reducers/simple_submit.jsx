import merge from 'lodash/object/merge'

export default function simple_submit ({ types }) {
  if (__DEBUG__ && (!Array.isArray(types) || types.length !== 3)) {
    throw new Error('Expected types to be an array of three elements.')
  }
  if (__DEBUG__ && (!types.every(t => typeof t === 'string'))) {
    throw new Error('Expected types to be strings.')
  }

  const [requestType, successType, failureType] = types

  return function updateItem (state = {
    isFetching: false,
    success: false,
    error: false
  }, action) {
    switch (action.type) {
      case requestType:
        return merge({}, state, {
          isFetching: true
        })
      case successType:
        return merge({}, state, {
          isFetching: false,
          success: true,
          response: action.response
        })
      case failureType:
        return merge({}, state, {
          isFetching: false,
          error: true,
          response: action.response
        })
      default:
        return state
    }
  }
}
