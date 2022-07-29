import React, { Component } from 'react';

class FilterItemsDropdownItem extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="timeline-filter-dropdown-item" onClick={() => this.props.onItemClick(this.props.label)}>
        <input
          type="checkbox"
          name='isChecked'
          id={this.props.label}
          checked={this.props.isChecked}
          readOnly
        />
        <span className={`timeline-filter-label ${this.props.type === 'insights' ? 'timeline-filter-label-insights' : ''}`} htmlFor={this.props.label}>
          {this.props.label}
        </span>
      </div>
    );
  }
}

export default FilterItemsDropdownItem;
