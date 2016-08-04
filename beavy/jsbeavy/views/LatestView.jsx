import React from 'react'
import { connect } from 'react-redux'
import { LIST } from 'reducers/list'

const Link = ({
  key,
  title,
  url
}) => (
  <li key={key}>
    <a target="_blank" href={url}>{title}</a>
  </li>
)

const LinksList = ({
  links
}) => (
  <ul>
    {links.map(l => 
      <Link key={l.id} {...l} />
    )}
  </ul>
)

const mapDataToEntities = (data, entities) => {
  return data.map((item) => {
    return entities[item.type][item.id]
  })
}

const mapStateToProps = (state) => {
  return {
    links: mapDataToEntities(
      state.list.data,
      state.entities
    )
  }
}

export default connect(
  mapStateToProps
)(LinksList)

