import React from 'react'
import { Link, Route } from 'react-router'
import { addExtension } from 'config/extensions'
import { make_url } from 'utils'

import CommentsView from './views/Comments'
import CommentView from './views/Comment'

// addExtension('MainMenuItem', function() {
//   return (<li><Link to='home'>other</Link> this comes from comments</li>)
// });

addExtension('userNavigationItems', function () {
  return <Link key='my-comments' to={make_url.account('comments/')}>My Comments</Link>
})
addExtension('accountRoutes',
  <Route key='comments' path='comments/' component={CommentsView} />)
addExtension('accountRoutes',
  <Route key='comment' path='comments/:commentId/' component={CommentView} />)
