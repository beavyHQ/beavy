import { compose, createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk';
import apiMiddleware from '../middleware/api';
import { getNamedExtensions, getExtensions, addManyExtensions, addExtension, addNamedExtension } from 'config/extensions';

addManyExtensions("storeMiddlewares", [thunkMiddleware, apiMiddleware]);

addNamedExtension("reducers", "CURRENT_USER", (x=null) => x)

export default function configureStore (initialState) {
  let middlewares = getExtensions("storeMiddlewares");
  if (__DEBUG__) {
    // we concat to make sure we aren't messing with
    // with the extensions list itself but create a copy
    const createLogger = require('redux-logger');
    middlewares = middlewares.concat([createLogger({
      level: 'info',
      collapsed: true
    })]);
  }

  let createStoreWithMiddleware = applyMiddleware.apply(this, middlewares);

  if (__REDUX_DEV_TOOLS__){
    const { devTools, persistState } = require('redux-devtools');
    createStoreWithMiddleware = compose(
        createStoreWithMiddleware,
        // Provides support for DevTools:
        devTools(),
        // Lets you write ?debug_session=<name> in address bar to persist debug sessions
        persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
      )
  }

  const store = createStoreWithMiddleware(createStore)(
      combineReducers(getNamedExtensions("reducers")), initialState);

  // if (module.hot) {
  //   module.hot.accept('../reducers', () => {
  //     const nextRootReducer = require('../reducers/index');

  //     store.replaceReducer(nextRootReducer);
  //   });
  // }
  return store;
}
