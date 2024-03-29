/* This runs several cleanup operations on our data before migration from Archivists' Toolkit to ArchivesSpace. It
 updates FileVersions Use Statements to Audio-Streaming, changed Digital Object Show attribute to onLoad instead of replace,
 replaces leftover xml namespaces from note contents, and sets instance and extent types for some stubborn items.
*/

UPDATE FileVersions SET useStatement='Audio-Streaming' WHERE useStatement='Audio streaming' OR useStatement='Audio-streaming' OR useStatement=’audio_streaming’;
UPDATE FileVersions SET eadDaoShow='replace' WHERE eadDaoShow='onLoad';
UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');
UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');
UPDATE ArchDescriptionInstances SET instanceType = "Graphic materials" WHERE resourceComponentId = 55585;
UPDATE ResourcesComponents SET extentType = "photograph(s)" WHERE resourceComponentId = 104406;
