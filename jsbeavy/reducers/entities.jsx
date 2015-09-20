// A JSONApi-Based data to entities reducer
// is able to find data.relationship.attributes
// into depth and merge them too

import merge from "lodash/object/merge"
import forEach from "lodash/collection/forEach"
import partial from "lodash/function/partial"
import map from "lodash/collection/map"

import { addNamedExtension } from 'config/extensions'

function entities(state = {}, action){
  if (action.response && action.response.entities){
    return merge({}, state, action.response.entities);
  }

  return state;
}


addNamedExtension("reducers", "entities", entities);