import { compose, createStore, combineReducers } from 'redux';
import { devTools } from 'redux-devtools';
import { getNamedExtensions,addNamedExtension } from 'config/extensions';

let createStoreWithMiddleware;

if (__DEBUG__) {
  createStoreWithMiddleware = compose(devTools())(createStore);
} else {
  createStoreWithMiddleware = createStore;
}

addNamedExtension("reducers", "CURRENT_USER", (x=null) => x)

export default function configureStore (initialState) {
  const store = createStoreWithMiddleware(
      combineReducers(getNamedExtensions("reducers")), initialState);

  // if (module.hot) {
  //   module.hot.accept('../reducers', () => {
  //     const nextRootReducer = require('../reducers/index');

  //     store.replaceReducer(nextRootReducer);
  //   });
  // }
  return store;
}
