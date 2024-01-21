from job.models import Job
from applicant.models import JobApplicantMessage,JobApplicantAppliedJob,JobApplicantActivity,JobApplicantFeedback,JobApplicantComment
from datetime import datetime

class JobApplicantManager:
    def __init__(self,applicant):
        self.applicant = applicant

    def create_job_applicant_message(self,message):
        if message.get('comm_id'):
            applicant_message = JobApplicantMessage()
            applicant_message.applicant = self.applicant
            applicant_message.comm_id = message.get('comm_id')
            applicant_message.comm_subject = message.get('comm_subject')
            applicant_message.comm_text = message.get('comm_text')
            applicant_message.comm_author_email = message.get('comm_author_email')
            applicant_message.comm_to = message.get('comm_to')
            applicant_message.comm_cc = message.get('comm_cc')
            applicant_message.comm_bcc = message.get('comm_bcc')
            if message.get('comm_datetime_sent'):
                applicant_message.comm_datetime_sent = datetime.strptime(message.get('comm_datetime_sent'), "%Y-%m-%d %H:%M:%S")
            applicant_message.save()
    
    def create_applicant_applied_job(self,job):
        job_instance = Job.objects.filter(job_id = job['job_id']).first()
        if job_instance:
            job_applied = JobApplicantAppliedJob()
            job_applied.applicant = self.applicant
            job_applied.job = job_instance
            job_applied.hiring_lead_rating = job['hiring_lead_rating']
            job_applied.average_rating = job['average_rating']
            job_applied.workflow_step_id = job['workflow_step_id']
            job_applied.job_title = job['job_title']
            job_applied.applicant_progress = job['applicant_progress']
            job_applied.save()
    
    def create_applicant_activity(self,activity):
        applicant_activity = JobApplicantActivity()
        applicant_activity.applicant = self.applicant
        applicant_activity.activity_id = activity['activity_id']
        applicant_activity.activity_on = datetime.strptime(f"{activity['date']} {activity['time']}", "%Y-%m-%d %H:%M:%S")
        applicant_activity.save()
    
    def create_job_applicant_feedback(self,feedback):
        applicant_feedback = JobApplicantFeedback()
        applicant_feedback.applicant = self.applicant
        applicant_feedback.feedback = feedback
        applicant_feedback.save()

    def create_job_applicant_comment(self,comment):
        applicant_comment = JobApplicantComment()
        applicant_comment.applicant = self.applicant
        applicant_comment.comment = comment
        applicant_comment.save()

