
"""テスト実行の結果を追跡するクラス。"""
class TestResult():
        def __init__(self):
            #正常カウント
            self.runCount = 0
            #異常カウント
            self.errorCount = 0
        # 各テストの開始時に呼び出される
        def testStarted(self):
            self.runCount = self.runCount + 1
        # テストが失敗するたびに呼び出される
        def testFailed(self):
            self.errorCount = self.errorCount + 1
        # 最終的な結果を提示する役割
        def summary(self):
            return f"{self.runCount} run, {self.errorCount} failed"

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
            print(f"{self.name}: PASSED") 
        except AssertionError:
            # assertの失敗をテスト失敗として捕捉
            result.testFailed()
            print(f"{self.name}: FAILED (AssertionError)") 
        except Exception:
            result.testFailed()
            print(f"{self.name}: FAILED (Exception)") 
        finally:
            # 例外の有無にかかわらず、必ずtearDownが実行される
            self.tearDown()

        

"""複数のテストケースをまとめて管理し、実行するためのクラス。"""
class TestSuite:
    def __init__(self):
        self.tests = []
    # テストオブジェクトを引数として受け取り、self.testsリストの末尾に追加
    def add(self,test):
        self.tests.append(test)
    # 実行されたテストの数や失敗数といったすべての結果を一つの場所で集計する
    def run(self,result):
        for test in self.tests:
            test.run(result)

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
        raise Exception("このテストは意図的に失敗します。")
    # tearDownメソッドが実行されたことをログに記録
    def tearDown(self):
        self.log = self.log + "tearDown "

"""テストフレームワークが正しく動作するかを検証するためのテスト用クラス。"""
class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()
    # setUpとtearDownメソッドが、メインのテストメソッドを囲む形で正しい順序で呼び出されているかを確認
    def testTemplateMethod(self):  
        test = WasRun("testMethod")
        # setUp、testMethod、tearDownが順番に呼び出される
        test.run(self.result)
        # log変数の最終的な文字列が期待される順序と完全に一致するかを確認
         # 3つのメソッドが正しい順序で、かつすべて実行されたことが証明される
        assert("setUp testMethod tearDown " == test.log)

    # テストが成功した際のTestResultの集計が正しいかをテストする。
    def testResult(self):
        # どのメソッドを実行するかを伝えている
        test = WasRun("testMethod")
        test.run(self.result)
        # TestResult オブジェクトが返すテスト結果の概要が、
        # 期待通りの文字列 "1 run, 0 failed" と一致するかを確認
        assert("1 run, 0 failed" == self.result.summary())

    # テストが失敗した際のTestResultの集計が正しいかをテストする。
    def testFailedResult(self):
        # 意図的に例外を発生させるように設計
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        # 最後の assert 文で、TestResult オブジェクトの summary() メソッドが返す文字列が、
        # 期待する結果である "1 run, 1 failed" と一致するかを確認
        assert("1 run, 1 failed" == self.result.summary())

    # TestResultのsummaryメソッドの出力形式が正しいかをテストする。
    def testFailedResultFormatting(self):
        # 意図的に例外を発生させるように設計
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        # summary メソッドが返す文字列が、期待する正確な書式
        #  "1 run, 1 failed" になっているかを検証
        assert("1 run, 1 failed" == self.result.summary())

    # 複数のテストをまとめて実行するTestSuiteが正しく機能するかをテストする。
    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        # 集計された結果（2つのテストが実行され、そのうち1つが失敗）を文字列として返す
        assert("2 run, 1 failed" == self.result.summary())
    
# この部分がテストフレームワークの実行を担っている。
suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()

# この行でTestSuiteのrunメソッドが呼び出され、テストが開始される
suite.run(result)
print(result.summary())
