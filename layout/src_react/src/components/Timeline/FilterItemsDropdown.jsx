import React, { Component } from 'react'
import FilterItemsDropdownItem from './FilterItemsDropdownItem'

class FilterItemsDropdown extends Component {

   constructor(props) {
       super(props)
       //console.log(this.props.options);
   }

   onItemClick = (label) => {
      //console.log(label);
      this.props.onSelect(label)
   }

   render() {
       return (
          <div className='timeline-filter-dropdown'>
            {this.props.options.map((option, i) =>
               <div key={option}>
                  <FilterItemsDropdownItem
                     type={this.props.type}
                     label={option}
                     onItemClick={this.onItemClick}
                     isChecked={this.props.selected.includes(option)}
                  />
                  { i !== this.props.options.length-1 && <div className='dropdown-divide-line'></div> }
               </div>
            )}
          </div>
       )
   }
}

export default FilterItemsDropdown;