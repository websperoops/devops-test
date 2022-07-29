import React from 'react'
import './summaryMetrics.css'; 

function Summary_Metric({ value, name, increase, isEqualToPrev }) {
 
    

  return (
    <div className="text-dark chart-container homepage-chart-container">
        <h1 id='title' className="text-capitalize summary-title">{name}</h1>
        <div className="d-flex flex-row justify-content-center align-items-center">
        <p id='subtitle' className="text-center summary-value font-weight-bold">{`${name==='Sales'?'$':''}${value}`}</p>
        <div className="arrow-margin" >
       
        {
           !isEqualToPrev && (
              (increase) ?
              
           <svg className="svg-style" viewBox="0 0 65 151" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
             <g id="BAP-(Desktop)" stroke="none" fill="none">
             <g id="Chart" transform="translate(-597.000000, -283.000000)" fill="#6ED492">
                 <polygon id="Path-8" points="597 346.5 629.5 283 662 346.5 639.5 346.5 639.5 434 619.5 434 619.5 346.5"></polygon>
             </g>
             </g>
           </svg> 
         :                
            <svg className="svg-style" viewBox="0 0 65 151" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
             <g id="BAP-(Desktop)" stroke="none" fill="none">
             <g id="Chart" transform="translate(-705.000000, -283.000000)" fill="#FE2B2B">
              <polygon id="Path-8" transform="translate(737.500000, 358.500000) rotate(180.000000) translate(-737.500000, -358.500000) " points="705 346.5 737.5 283 770 346.5 747.5 346.5 747.5 434 727.5 434 727.5 346.5"></polygon>
             </g>
             </g>
            </svg>
           )
        }
            
            
        </div>
        </div>
    </div>
)
}

export default Summary_Metric;
