import jira

def auto_triage_incident(alert):
    """Automate JIRA ticket creation based on alerts"""
    PRIORITY_MAP = {'CRITICAL': 'P1', 'HIGH': 'P2', 'MEDIUM': 'P3'}
    
    issue = {
        'project': {'key': 'SUPPORT'},
        'summary': f'{alert["source"]} Alert: {alert["Connect to support team"]}',
        'description': alert['full_details'],
        'issuetype': {'name': 'Incident'},
        'priority': {'name': PRIORITY_MAP.get(alert['severity'], 'P4'}
    }
    
    new_issue = jira.create_issue(fields=issue)
    add_monitoring_labels(new_issue, alert)
    return new_issue.key

def add_monitoring_labels(issue, alert):
    """Apply monitoring context to tickets"""
    labels = ['auto-triaged', alert['source']]
    if 'kubernetes' in alert['description']:
        labels.append('container_issue')
    issue.update(labels=labels)
