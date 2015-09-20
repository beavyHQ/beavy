// A JSONApi-Based data to entities reducer
// is able to find data.relationship.attributes
// into depth and merge them too

import merge from "lodash/object/merge"
import forEach from "lodash/collection/forEach"
import partial from "lodash/function/partial"
import map from "lodash/collection/map"

import { addNamedExtension } from 'config/extensions'

export function extract_entities(input){
  // console.log("IN", input);
  const entitiesMap = {},
        addToMap = (x) =>  {
          // console.log("atm", x);
          if(!entities[x.type]) entitiesMap[x.type] = {};
          entitiesMap[x.type][x.id] = x;
        },
        addAttributesToMap = (x) => {
          // console.log("aa", x)
          if (x.attributes){
            addToMap(merge({type: x.type, id: x.id},
                            x.attributes))
          }
        },
        extract_relationships = (data) => {
          forEach(data.relationships || {}, (n, key) => {
            // console.log(n, key);
            if (Array.isArray(n)){
              forEach(n, addAttributesToMap)
            } else {
              addAttributesToMap(n)
            }
          });
        };

  if (input.included){
    forEach(input.included, addToMap);
  }

  if (input.data) {
    if (Array.isArray(input.data)) {
      forEach(input.data, x => {
        addAttributesToMap(x);
        extract_relationships(x);
      });
    } else {
      addAttributesToMap(input.data);
      extract_relationships(input.data);
    }
  }
  console.log("returning", entitiesMap);
  return entitiesMap;
}

function entities(state = {}, action){
  if (action.response && (action.response.data || action.response.included)){
    return merge({}, state, extract_entities(action.response));
  }

  return state;
}


addNamedExtension("reducers", "entities", entities);