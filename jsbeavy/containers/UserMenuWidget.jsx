import React from "react";
import { Link } from "react-router";
import ReactLogo from "elements/ReactLogo";
import { Modal } from "components/Modal";
import { make_url } from 'utils';
import { connect } from 'react-redux';
import {openLogin, openRegister} from 'actions/user_modal'
// import styles from './MainMenu.scss';
import classnames from 'classnames';


const mapDispatchToProps = (state) => ({
  is_authenticated: !!state.CURRENT_USER,
  user : state.CURRENT_USER || {}
});

export class UserMenuWidget extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func,
    is_authenticated : React.PropTypes.bool,
    user : React.PropTypes.object
  }

  renderLoggedOut(){
    if (config.SECURITY_REGISTERABLE)
        return <div>
                  <button onClick={(e) => this.props.dispatch(openLogin())}>
                    Login
                  </button>
                  <button onClick={(e) => this.props.dispatch(openRegister())}>
                    Sign up
                  </button>
                </div>;
      else
        return <button onClick={(e) => this.props.dispatch(openLogin())}>
                  Login
               </button>;
  }

  render() {
    if (!this.props.is_authenticated) return this.renderLoggedOut()

    return <Link to={make_url.users(this.props.user.id)}>Me</Link>;
  }
}

export default connect(mapDispatchToProps)(UserMenuWidget);
