import React, { PropTypes } from 'react'
import { MainMenu, styles as MainMenuStyles } from 'components/MainMenu'
import UserModal from 'containers/UserModal'
import UserMenuWidget from 'containers/UserMenuWidget'

import { make_url } from 'utils'
import { Link } from 'react-router'

import styles from './styles/hn_styles.scss'
import { setupViews } from './setup'
import { FormattedMessage } from 'react-intl'

setupViews()

// overwrite behaviour of the logo styles
Object.assign(MainMenuStyles, {logo: styles.logo, title: styles.title})

// insertExtension("MainNavigationTools", 0, () => <UserMenuWidget />)

export default class HackerNewsApplication extends React.Component {
  static propTypes = {
    children: PropTypes.object
  }
  render () {
    return <div className={styles.hackerNews}>
              <UserModal />
              <MainMenu
                styles={MainMenuStyles}
                logo='http://svgporn.com/logos/ycombinator.svg'
                navigationTools={<UserMenuWidget />}
              >
                <Link to={make_url.account('comments/')}>
                  <FormattedMessage id='threads' defaultMessage='threads'/></Link>
               | <Link to='/submit/'><FormattedMessage id='submit' defaultMessage='submit'/></Link>

              </MainMenu>
              {this.props.children}
            </div>
  }
}
