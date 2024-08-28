from app.core.usecases.impl.token_processor_usercase_impl import TokenProcessorUseCaseImpl


class TestGateway2:
  def __init__(self, token_gateway: TokenProcessorUseCaseImpl):
    self.token_gateway = token_gateway

  def get_name(self):
    self.token_gateway.printTest()