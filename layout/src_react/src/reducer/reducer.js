function Reducer(state, action) {
    switch (action.type) {
        case 'initialLoad':
            {
                return {
                    ...state,
                    charts: action.payload
                }
            }

        case 'chartAdd':
            {
                return {
                    ...state,
                    charts: [...state.charts, action.payload]
                }
            }

        case 'chartJson':
            {
                return {
                    ...state,
                    chartsJson: [...state.chartsJson, action.payload]
                }
            }

        case 'chartUpdate':
            {
                return {
                    ...state,
                    chartUpdate: action.payload
                }
            }

        case 'chartDelete':
            {
                return {
                    ...state,
                    chartDelete: action.payload
                }
            }

        case 'chartFavorite':
            {
                return {
                    ...state,
                    chartFavorite: action.payload
                }
            }

        case 'chartDetails':
            {
                return {
                    ...state,
                    chartDetails: action.payload
                }
            }


        default:
            {
                return state
            }
    }
}

export default Reducer