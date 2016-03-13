import React, { PropTypes } from 'react'
import { MainMenu } from 'components/MainMenu'
import UserModal from 'containers/UserModal'
import UserMenuWidget from 'containers/UserMenuWidget'

import { getExtensions } from 'config/extensions'

export default class Application extends React.Component {
  static propTypes = {
    children: PropTypes.object
  }
  render () {
    return <div>
            <UserModal />
            <MainMenu
              logo='http://svgporn.com/logos/kong.svg'
              navigationTools={<UserMenuWidget />} >
              {getExtensions('MainMenuItem').map(x => x.call(this))}
            </MainMenu>
            {this.props.children}
          </div>
  }
}
