import React, { PropTypes } from 'react'
import { MainMenu } from 'components/MainMenu'

import UserModal from 'containers/UserModal'
import UserMenuWidget from 'containers/UserMenuWidget'

import { getExtensions } from 'config/extensions'

import styles from './styles/twitterApp.scss'

export default class Application extends React.Component {
  static propTypes = {
    loading: PropTypes.bool.isRequired,
    children: PropTypes.array
  }
  static getProps (stores, params) {
    var transition = stores.Router.getItem('transition')
    return {
      loading: !!transition
    }
  }
  render () {
    var { loading } = this.props
    return <div className={styles.this + (loading ? ' ' + styles.loading : '')}>
          <div className={styles.loadingElement}>loading...</div>
          <UserModal />
          <MainMenu
            title='Twitter'
            logo='http://svgporn.com/logos/twitter.svg'
            navigationTools={<UserMenuWidget />}
          >
              {getExtensions('MainMenuItem').map(x => x.call(this))}
          </MainMenu>
          {this.props.children}
      </div>
  }
}
