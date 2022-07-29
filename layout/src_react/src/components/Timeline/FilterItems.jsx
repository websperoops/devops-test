import React, { Component,Fragment } from 'react'
import FilterItemsDropdown from './FilterItemsDropdown'
import { getIntegrationsList } from '../../api/BLApi'

class FilterItems extends Component {

    constructor(props) {
        super(props)

        this.options = []

        this.state = {
            selected: [],
            showDropdown: false
        }

        this.setSelected = this.setSelected.bind(this)

        this.setWrapperRef = this.setWrapperRef.bind(this);
        this.handleClickOutside = this.handleClickOutside.bind(this);
    }

    setWrapperRef(node) {
        this.wrapperRef = node;
    }

    handleClickOutside(event) {
        if (this.wrapperRef && !this.wrapperRef.contains(event.target)) {
            this.setState({showDropdown: false})
        }
    }

    componentDidMount() {
        document.addEventListener('mousedown', this.handleClickOutside);
    }
    
    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside);
    }

    toggleDropdown = () => {
        if(this.props.options.length > 0) this.setState(prevState => { return { showDropdown: !prevState.showDropdown } })
    }

    setSelected(option) {
        let filtered
        if(this.state.selected.includes(option)){
            filtered = this.state.selected.filter(item => item != option)
        } else {
            filtered = [...this.state.selected, option]
        }

        this.setState({selected: filtered})
        this.props.filterItemsFunc(filtered)
        // this.props.filterItemsFunc(filtered.map(item => {
        //     return {label: item, value: item.toLowerCase()}
        // }))
    }

    render() {  
        const {type, options} = this.props
      
        return (
            <Fragment>
                <span className={`timeline-homepage-header-dropdown timeline-dropdown-${type}`} ref={this.setWrapperRef}>
                    <span
                        className='homepage-header-dropdown-block timeline-homepage-header-dropdown-block'
                        onClick={this.toggleDropdown}
                        style={{overflow: 'hidden', textOverflow: 'ellipsis'}}
                    >
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                    </span>
                    {
                        this.state.showDropdown &&
                            <FilterItemsDropdown
                                options={options}
                                selected={this.state.selected}
                                onSelect={this.setSelected}
                                type={type}
                            />
                    }
                </span>
            </Fragment>
        )
      }
}

export default FilterItems;