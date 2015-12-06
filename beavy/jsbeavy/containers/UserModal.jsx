import React from 'react'
import { Modal } from 'components/Modal'
import config from 'config/config'
import { closeModal } from 'actions/user_modal'
import { USER_MODAL } from 'reducers/user_modal'
import { connect } from 'react-redux'

// import styles from './MainMenu.scss';
import classnames from 'classnames'

function mapDispatchToProps (state) {
  return {
    user : state.CURRENT_USER,
    is_authenticated : !!state.CURRENT_USER,
    showModal: state[USER_MODAL] || ''
  } };

export class UserModal extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func,
    is_authenticated : React.PropTypes.bool,
    user : React.PropTypes.object,
    showModal: React.PropTypes.string
  }
  render () {
    if (this.props.user || !this.props.showModal) return null
    let url = '/login'
    if (this.props.showModal === 'REGISTER') {
      url = '/register'
    }

    return <Modal onRequestClose={(e) => this.props.dispatch(closeModal())}>
            <iframe src={url}></iframe>
          </Modal>
  }
}

export default connect(mapDispatchToProps)(UserModal)
