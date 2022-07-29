import React, { useReducer, useState, useEffect, useLayoutEffect, Suspense, Component } from 'react'
import DashWidgetContent from './DashWidgetContent';
import DashWidgetTopPanel from './DashWidgetTopPanel';
import _ from 'lodash'

class DashWidget extends Component {
	shouldComponentUpdate(prevProps, prevState) {
		if (!_.isEqual(prevProps, this.props)) { //only update the component if the new props are different than the current props.
			return true
		}
		return false
	}

	render() {
		return (
			<div className="graph theme-widgets">
				<DashWidgetTopPanel
					{...this.props}
				/>
				<DashWidgetContent
					{...this.props}
				/>
			</div>

		)
	}
}

export default DashWidget;
