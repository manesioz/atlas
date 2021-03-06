
from foundations_spec.extensions import let_fake_redis
from foundations_spec import *
from foundations_events.consumers.single_project_metric import SingleProjectMetric


class TestSingleProjectMetric(Spec):

    mock_redis = let_fake_redis()

    @let
    def consumer(self):
        return SingleProjectMetric(self.mock_redis)

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def project_name(self):
        return self.faker.name()

    @let
    def metric_key(self):
        return self.faker.name()
    
    @let
    def metric_value(self):
        return self.faker.random.randint(1, 230)

    @let
    def random_timestamp(self):
        return self.faker.random.randint(1, 230)

    def test_call_adds_new_metric_to_redis_with_project_name_and_job_id(self):
        from foundations_internal.fast_serializer import deserialize

        message = {
            'key': self.metric_key, 
            'value': self.metric_value, 
            'job_id': self.job_id, 
            'project_name': self.project_name
        }
        
        self.consumer.call(message, self.random_timestamp, None)
        project_metric = self.mock_redis.hgetall(f'projects:{self.project_name}:metrics:{self.metric_key}')
        
        serialized_metric = project_metric[self.job_id.encode()]
        metric = deserialize(serialized_metric)
        
        self.assertEqual((self.random_timestamp, self.metric_value), metric)
