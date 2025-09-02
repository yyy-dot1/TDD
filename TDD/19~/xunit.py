"""テスト実行の結果を追跡するクラス。"""
class TestResult():
        def __init__(self):
            #正常カウント
            self.runCount = 0
            #異常カウント
            self.errorCount = 0
        
        def testStarted(self):
            self.runCount = self.runCount + 1
        def testFailed(self):
            self.errorCount = self.errorCount + 1
        # 結果
        def summary(self):
            return "%d run,%d failed" %(self.runCount,self.errorCount)

"""単一のテストケースを定義するための基底クラス。"""
class TestCase:
    def __init__(self,name):
        self.name = name
    # テストメソッドを実行する前に呼び出されるセットアップメソッド。
    def setUp(self):
        pass
     # テストメソッドの実行後に必ず呼び出されるクリーンアップメソッド。
    def tearDown(self):
        pass
    # テストメソッドを実行し、結果をTestResultオブジェクトに記録する。
    def run(self,result):
        result.testStarted()
        self.setUp()
        try:
            # 指定されたテストメソッドを取得して実行する
            method = getattr(self,self.name)
            method()
        except:
            result.testFailed()
        # tearDownは、例外の有無にかかわらず必ず実行されるように
        self.tearDown()

"""実行用クラス。テスト対象のコードを模倣している。"""
class WasRun(TestCase):
    # 実行されたことを示すテストメソッド。
    def setUp(self):
        # setUpメソッドが実行されたことをログに記録
        self.log = "setUp "
    # テストメソッドが実行されたことをログに記録
    def testMethod(self):
        self.log = self.log + "testMethod "
    # 意図的に例外を発生させ、テスト失敗をシミュレートする。
    def testBrokenMethod(self):
        raise Exception
    # tearDownメソッドが実行されたことをログに記録
    def tearDown(self):
        self.log = self.log + "tearDown "

"""テストフレームワークが正しく動作するかを検証するためのテスト用クラス。"""
class TestCaseTest(TestCase):
    # runメソッドのテンプレートメソッドパターン（setUp, tearDownの呼び出し順序）をテストする。
    def testTemplateMethod(self):  
        test = WasRun("testMethod")
        test.run()
        assert("setUp testMethod tearDown " == test.log)

    # テストが成功した際のTestResultの集計が正しいかをテストする。
    def testResult(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 0 failed" == result.summary())

    # テストが失敗した際のTestResultの集計が正しいかをテストする。
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert("1 run, 1 failed" == result.summary())

    # TestResultのsummaryメソッドの出力形式が正しいかをテストする。
    def testFailedResultFormatting(self):
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert("1 run,1 failed" == result.summary())

    # 複数のテストをまとめて実行するTestSuiteが正しく機能するかをテストする。
    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        result = TestResult()
        suite.run(result)
        assert("2 run,1 failed" == result.summary())
    
"""複数のテストケースをまとめて管理し、実行するためのクラス。"""
class TestSuite:
    def __init__(self):
        self.tests = []
    
    def add(self,test):
        self.tests.append(test)

    def run(self,result):
        for test in self.tests:
            test.run(result)
    
suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print(result.summary())