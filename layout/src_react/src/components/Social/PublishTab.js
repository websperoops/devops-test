import React, { useContext } from 'react'
import PublishMyHistory from './PublishMyHistory'
import PublishSchedule from './PublishSchedule'
import PublishDrafts from './PublishDrafts'
import { SocialData } from './SocialContainer'
const PublishTab = () => {
    const { publishLink } = useContext(SocialData);

    return (
        <div style={{ backgroundColor: '#fff', minHeight: '600px' }} >
            {
                publishLink === "My History" && <PublishMyHistory /> ||
                publishLink === "Schedule" && <PublishSchedule /> ||
                publishLink === "Drafts" && <PublishDrafts />
            }
        </div>
    )
}

export default PublishTab