import React from 'react'
import { addExtension, getExtensions } from 'config/extensions'
import { Route } from 'react-router'
import { make_url } from 'utils'

import UserView from 'views/UserView'
import HomeView from 'views/HomeView'

export default function setupViews (Application) {
  addExtension('routes',
      <Route key='hello' name='hello' path='/' component={HomeView} />)

  addExtension('routes',
      <Route key='user' name='user' path={make_url.users('/:userId/')} component={UserView}>
        {getExtensions('userRoutes')}
      </Route>)

  addExtension('routes',
      <Route key='account' name='account' path={make_url.account('')}>
        {getExtensions('accountRoutes')}
      </Route>)
}
