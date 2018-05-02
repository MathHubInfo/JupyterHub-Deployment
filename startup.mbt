controller.handleLine("extension info.kwarc.mmt.api.web.REPLServer")
controller.handleLine("extension info.kwarc.mmt.interviews.InterviewServer")
controller.handleLine("extension info.kwarc.mmt.api.ontology.RelationalReader")
try {
controller.handleLine("lmh root/content/MathHub/")
controller.handleLine("lmh install MitM/smglom")
controller.handleLine("lmh install MitM/MoSIS")
} catch {
  case e : Throwable => println(e)
}
controller.handleLine("server on 9000 0.0.0.0")
