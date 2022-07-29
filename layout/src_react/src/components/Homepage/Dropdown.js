import React, { useEffect, useRef, Fragment } from 'react';

const useOutsideClick = (ref, callback) => {
    const handleClick = e => {
        if (ref.current &&!ref.current.contains(e.target)){
            callback()
        }
    }
    useEffect(()=>{
        document.addEventListener('click', handleClick)

        return () => {
            document.removeEventListener('click', handleClick)
        }
    })
}

const Dropdown = ({ toggleDropdown, options, type, clickTime, link }) => {
    const ref = useRef();

    useOutsideClick(ref, () => {
        toggleDropdown()
    })

    const showOptions = () => {
        return options.map((option,i) => {
            return (
                <Fragment key={option}>
                    {
                        type==='post' ? 
                        (
                            <div className='view-post'
                                onClick={()=>{
                                    window.open(link, '_blank')
                                    toggleDropdown()
                                }}
                                key={option}
                            >
                                {option}
                            </div>
                        )
                        :
                        (
                            <div className="select-time" key={option} onClick={()=>clickTime(option)}>{option}</div>
                        )
                    }
                    {
                      i !== options.length-1 && <div className='dropdown-divide-line'></div>
                    }
                </Fragment>
            )
        })
    }

    return (
        <div className='homepage-dropdown dropdown' ref={ref}>
            {showOptions()}
        </div>
    );
};

export default Dropdown;
