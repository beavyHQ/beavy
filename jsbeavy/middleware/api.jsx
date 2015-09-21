import merge from "lodash/object/merge";
import forEach from "lodash/collection/forEach";
import map from "lodash/collection/map";
import 'isomorphic-fetch';

import entites from 'reducers/entities';

// loosely based on the awesome redux real-world example from
// https://github.com/rackt/redux/blob/master/examples/real-world/middleware/api.js

export function format_jsonapi_result(input, key){
  const entitiesMap = {},
        result = {},
        output = {
          entities: entitiesMap,
        },
        addToMap = (x) =>  {
          if(!entitiesMap[x.type]) entitiesMap[x.type] = {};
          entitiesMap[x.type][x.id] = x;
        },
        addAttributesToMap = (x) => {
          if (x.attributes){
            addToMap(merge({type: x.type, id: x.id},
                            x.attributes))
          }
        },
        extract_relationships = (data) => {
          forEach(data.relationships || {}, (n, key) => {
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

  if (input.meta){ result.meta = input.meta };
  if (input.links){ result.links = input.links };

  if (input.data) {
    if (Array.isArray(input.data)) {
      result.data = [];
      forEach(input.data, x => {
        result.data.push({type: x.type, id: x.id});
        addAttributesToMap(x);
        extract_relationships(x);
      });
    } else {
      result.data = input.data;
      addAttributesToMap(input.data);
      extract_relationships(input.data);
    }
  }
  output[key] = result;
  return output;
}



// Fetches an API response and normalizes the result JSON according to schema.
// This makes every API response have the same shape, regardless of how nested it was.
function callApi(endpoint, key) {
  return fetch(endpoint, {
      credentials: 'same-origin', // keep the cookies for the session!
      headers: { // we always ask for json
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then(response =>
      response.json().then(json => ({ json, response }))
    ).then(({ json, response }) => {
      if (!response.ok) {
        return Promise.reject(json);
      }

      return Object.assign({}, format_jsonapi_result(json, key));
    });
}


// Action key that carries API call info interpreted by this Redux middleware.
export const CALL_API = Symbol('Call API');

// A Redux middleware that interprets actions with CALL_API info specified.
// Performs the call and promises when such actions are dispatched.
export default store => next => action => {
  const callAPI = action[CALL_API];
  if (typeof callAPI === 'undefined') {
    return next(action);
  }

  let { endpoint } = callAPI;
  const { key, types } = callAPI;

  if (typeof endpoint === 'function') {
    endpoint = endpoint(store.getState());
  }

  if (typeof endpoint !== 'string') {
    throw new Error('Specify a string endpoint URL.');
  }
  if (!key) {
    throw new Error('Specify a result key.');
  }
  if (!Array.isArray(types) || types.length !== 3) {
    throw new Error('Expected an array of three action types.');
  }
  if (!types.every(type => typeof type === 'string')) {
    throw new Error('Expected action types to be strings.');
  }

  function actionWith(data) {
    const finalAction = Object.assign({}, action, data);
    delete finalAction[CALL_API];
    return finalAction;
  }

  const [requestType, successType, failureType] = types;
  next(actionWith({ type: requestType }));

  return callApi(endpoint, key).then(
    response => next(actionWith({
      response,
      type: successType
    })),
    error => next(actionWith({
      type: failureType,
      error: error.message || 'Something bad happened'
    }))
  );
};
