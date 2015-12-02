import React from "react";
import { Link, Route } from "react-router";
import { connect } from "react-redux";
import { addExtension } from 'config/extensions';
import { make_url } from 'utils';


import { loadUserLikes } from './actions';
import UserLikesView from './views/UserLikes';

class MenuItem extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func
  }

  render() {
    console.log("rendering");
    return (<li><a onClick={(e) => this.props.dispatch(loadUserLikes(1))}>home</a>Test</li>)
  }

}

const ConnectedMenuItem = connect()(MenuItem);

addExtension("MainMenuItem", () => <ConnectedMenuItem key="connecteMenuItem"/>);
addExtension("userMenu", (function() {return <Link key="likes" to={make_url.users(this.props.userId + "/likes/")}> Likes </Link>;}));
addExtension("userRoutes", <Route key="likes" path="likes/" component={UserLikesView} /> );
